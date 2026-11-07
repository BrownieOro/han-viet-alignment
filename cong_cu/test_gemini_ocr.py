"""Run with python3 -m unittest discover -s cong_cu -p 'test_*.py'. No API calls."""
import io
import json
import unittest
from unittest.mock import patch
from urllib.error import HTTPError

import gemini_ocr


class GeminiOCRTests(unittest.TestCase):
    def setUp(self):
        self.data = {'apiKey': 'test_key_without_real_credentials', 'model': 'gemini-3.5-flash',
                     'language': 'vie', 'layout': '3', 'image': '/9j/'}

    def test_success_sends_one_page_with_key_in_header(self):
        result = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': 'Tiếng Việt'}]}}]}
        with patch('gemini_ocr.request.urlopen') as call:
            call.return_value.__enter__.return_value = io.StringIO(json.dumps(result))
            status, response = gemini_ocr.recognize(self.data)
        self.assertEqual((status, response['text']), (200, 'Tiếng Việt'))
        self.assertEqual(call.call_count, 1)
        req = call.call_args.args[0]
        self.assertNotIn(self.data['apiKey'], req.full_url)
        self.assertEqual(req.get_header('X-goog-api-key'), self.data['apiKey'])

    def test_auth_key_with_dots_and_long_value_reaches_google(self):
        key = 'AQ.' + 'a' * 300 + '.signature_123'
        data = {**self.data, 'apiKey': '  ' + key + '\n'}
        result = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': 'Văn bản'}]}}]}
        with patch('gemini_ocr.request.urlopen') as call:
            call.return_value.__enter__.return_value = io.StringIO(json.dumps(result))
            status, response = gemini_ocr.recognize(data)
        self.assertEqual(status, 200)
        self.assertEqual(response['text'], 'Văn bản')
        self.assertEqual(call.call_args.args[0].get_header('X-goog-api-key'), key)

    def test_empty_manual_key_uses_local_file(self):
        result = {'candidates': [{'finishReason': 'STOP', 'content': {'parts': [{'text': 'Văn bản'}]}}]}
        with patch('gemini_ocr.local_key', return_value=self.data['apiKey']), patch('gemini_ocr.request.urlopen') as call:
            call.return_value.__enter__.return_value = io.StringIO(json.dumps(result))
            status, response = gemini_ocr.recognize({**self.data, 'apiKey': ''})
        self.assertEqual(status, 200)
        self.assertEqual(call.call_args.args[0].get_header('X-goog-api-key'), self.data['apiKey'])
        body = json.loads(call.call_args.args[0].data)
        self.assertEqual(body['generationConfig']['thinkingConfig']['thinkingLevel'], 'minimal')
        self.assertEqual(call.call_args.kwargs['timeout'], 30)

    def test_overloaded_model_does_not_retry_automatically(self):
        failure = {'error': {'message': 'This model is currently experiencing high demand.'}}
        upstream = HTTPError('https://example.test', 503, 'overloaded', {}, io.BytesIO(json.dumps(failure).encode()))
        with patch('gemini_ocr.request.urlopen', side_effect=upstream):
            status, response = gemini_ocr.recognize(self.data)
        self.assertEqual(status, 503)
        self.assertFalse(response['retryable'])
        self.assertIn('quá tải', response['error'])

    def test_daily_quota_stops_and_redacts_key(self):
        failure = {'error': {'message': 'Quota exceeded ' + self.data['apiKey'], 'details': [
            {'quotaId': 'GenerateRequestsPerDayPerProjectPerModel-FreeTier'}, {'retryDelay': '5s'}]}}
        upstream = HTTPError('https://example.test', 429, 'quota', {}, io.BytesIO(json.dumps(failure).encode()))
        with patch('gemini_ocr.request.urlopen', side_effect=upstream):
            status, response = gemini_ocr.recognize(self.data)
        self.assertEqual(status, 429)
        self.assertFalse(response['retryable'])
        self.assertNotIn(self.data['apiKey'], str(response))

    def test_minute_limit_can_retry(self):
        failure = {'error': {'details': [{'quotaId': 'RequestsPerMinute'}, {'retryDelay': '12s'}]}}
        upstream = HTTPError('https://example.test', 429, 'quota', {}, io.BytesIO(json.dumps(failure).encode()))
        with patch('gemini_ocr.request.urlopen', side_effect=upstream):
            status, response = gemini_ocr.recognize(self.data)
        self.assertEqual(status, 429)
        self.assertTrue(response['retryable'])
        self.assertEqual(response['retryAfter'], 12)

    def test_truncated_output_is_not_marked_successful(self):
        result = {'candidates': [{'finishReason': 'MAX_TOKENS', 'content': {'parts': [{'text': 'partial'}]}}]}
        with patch('gemini_ocr.request.urlopen') as call:
            call.return_value.__enter__.return_value = io.StringIO(json.dumps(result))
            self.assertEqual(gemini_ocr.recognize(self.data)[0], 422)

    def test_invalid_input_does_not_contact_google(self):
        for field, value in [('apiKey', 'bad\r\nkey'), ('model', 'unapproved'), ('image', 'bad-base64')]:
            with self.subTest(field=field), patch('gemini_ocr.request.urlopen') as call:
                data = {**self.data, field: value}
                self.assertEqual(gemini_ocr.recognize(data)[0], 400)
                call.assert_not_called()

    def test_oversized_request_does_not_contact_google(self):
        with patch('gemini_ocr.MAX_REQUEST_BYTES', 100), patch('gemini_ocr.request.urlopen') as call:
            self.assertEqual(gemini_ocr.recognize(self.data)[0], 413)
            call.assert_not_called()


if __name__ == '__main__':
    unittest.main()
