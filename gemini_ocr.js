/* Optional Gemini OCR. A manual key stays in this page; the local key stays on the server. */
(() => {
    const $ = id => document.getElementById(id);
    const settings = document.createElement('div');
    settings.innerHTML = `
        <label for="ocrEngine">Công cụ OCR</label>
        <select id="ocrEngine"><option value="tesseract">Tesseract · trên trình duyệt</option><option value="gemini">Gemini · gửi ảnh trang lên Google</option></select>
        <div id="geminiSettings" hidden>
            <label for="geminiKey">Gemini API key · chỉ giữ trong phiên đang mở</label>
            <input id="geminiKey" type="password" autocomplete="off" spellcheck="false" style="width:min(100%,450px)" placeholder="Để trống để dùng file .gemini_api_key ở máy">
            <button id="geminiShowKey" type="button">Hiện key</button>
            <button id="geminiClearKey" type="button">Xóa key</button>
            <p id="geminiKeyStatus" class="muted">Đang kiểm tra file key local…</p>
            <label for="geminiModel">Model</label>
            <select id="geminiModel"><option value="gemini-3.5-flash-lite">Gemini 3.5 Flash-Lite · ưu tiên tốc độ</option><option value="gemini-3.5-flash">Gemini 3.5 Flash</option></select>
            <p class="muted">Dùng key thuộc project Free tier chưa bật billing. Tool không xác nhận được gói thanh toán từ API key. Mỗi trang gửi một request thường đến Google. Nội dung gửi qua free tier có thể được Google dùng để cải thiện sản phẩm.</p>
            <p class="muted">Giới hạn của tool · 50 trang/lượt, request dưới 15 MB. Bấm Chạy OCR để thử trang hiện tại. <a href="https://aistudio.google.com/" target="_blank" rel="noopener noreferrer">Xem RPD/RPM/TPM trong AI Studio</a> · chọn đúng project và model ở Usage / Rate limits.</p>
            <p id="geminiCount" class="muted">Phiên này đã gửi 0 lần gọi OCR qua server local, gồm retry. Đây không phải quota còn lại trên Google.</p>
            <button id="geminiResume" hidden>Tiếp tục lượt Gemini</button>
        </div>`;
    $('ocrProgress').parentElement.prepend(settings);
    fetch('/api/gemini-config').then(async response => {
        if (!response.ok) throw Error('Khởi động lại server Python để đọc key local.');
        return response.json();
    }).then(config => {
        $('geminiKeyStatus').textContent = config.localKeyConfigured
            ? 'Đã có key local. Bạn có thể để trống ô key và chạy OCR.'
            : 'File .gemini_api_key chưa có key. Dán key vào file rồi lưu, hoặc nhập ở ô phía trên.';
    }).catch(error => { $('geminiKeyStatus').textContent = error.message; });
    let busy = false;
    let stopped = false;
    let sent = 0;
    let job = null;
    let wakeWait = null;
    const originalRun = $('ocrRun').onclick;
    const originalRange = $('ocrRange').onclick;
    const originalStop = $('ocrStop').onclick;
    const originalDownload = $('ocrDownload').onclick;
    let geminiOutput = false;
    const lockedIds = ['ocrEngine', 'geminiKey', 'geminiModel', 'geminiShowKey', 'geminiClearKey',
        'book', 'page', 'prev', 'next', 'go', 'addInput', 'ocrLang', 'ocrLayout', 'ocrFrom', 'ocrTo', 'oldResult'];

    $('ocrEngine').onchange = () => {
        const gemini = $('ocrEngine').value === 'gemini';
        $('geminiSettings').hidden = !gemini;
        $('ocrProgress').textContent = gemini
            ? 'Gemini gửi ảnh từng trang lên Google. Dùng key local hoặc nhập key, rồi chọn trang để chạy.'
            : 'Tesseract chạy trong trình duyệt. Lần đầu cần mạng tải mô hình.';
    };
    $('geminiShowKey').onclick = () => {
        const hidden = $('geminiKey').type === 'password';
        $('geminiKey').type = hidden ? 'text' : 'password';
        $('geminiShowKey').textContent = hidden ? 'Ẩn key' : 'Hiện key';
    };
    $('geminiClearKey').onclick = () => { $('geminiKey').value = ''; };

    function signature(from, to) {
        return JSON.stringify([$('book').value, from, to, $('ocrLang').value, $('ocrLayout').value]);
    }

    async function sendPage(canvas) {
        const image = canvas.toDataURL('image/jpeg', 0.95).split(',')[1];
        const body = JSON.stringify({apiKey: $('geminiKey').value.trim(), model: job.model,
            language: job.language, layout: job.layout, image});
        const size = new TextEncoder().encode(body).length;
        if (size >= 14_900_000) throw Error(`Request ${(size / 1_000_000).toFixed(1)} MB quá lớn. Giới hạn tool là 15 MB kể cả dữ liệu mã hóa.`);
        for (let attempt = 0; attempt < 3; attempt++) {
            if (stopped) return null;
            sent++;
            $('geminiCount').textContent = `Phiên này đã gửi ${sent} lần gọi OCR qua server local, gồm retry. Đây không phải quota còn lại trên Google.`;
            const controller = new AbortController();
            const started = Date.now();
            const showWaiting = () => {
                $('ocrProgress').textContent = `Trang ${job.next} · đang chờ ${job.model} · ${Math.floor((Date.now() - started) / 1000)} giây (tối đa 35 giây).`;
            };
            showWaiting();
            const ticker = setInterval(showWaiting, 1000);
            const timeout = setTimeout(() => controller.abort(), 35000);
            let response;
            let result;
            try {
                response = await fetch('/api/gemini-ocr', {method: 'POST', headers: {'Content-Type': 'application/json'}, body, signal: controller.signal});
                try { result = await response.json(); }
                catch (error) {
                    if (error.name === 'AbortError') throw error;
                    throw Error(`Server trả dữ liệu không hợp lệ (HTTP ${response.status}). Hãy khởi động lại server Python của project.`);
                }
            } catch (error) {
                if (error.name === 'AbortError') throw Error('Đã chờ 35 giây. Dừng chờ request này, có thể đổi model rồi tiếp tục. Google có thể vẫn xử lý request đã gửi.');
                if (error instanceof TypeError) throw Error('Mất kết nối server local. Kiểm tra cửa sổ chạy Python rồi tiếp tục trang này.');
                throw error;
            } finally {
                clearTimeout(timeout);
                clearInterval(ticker);
            }
            if (response.ok) {
                job.lastSeconds = ((Date.now() - started) / 1000).toFixed(1);
                return result.text;
            }
            const message = [result.error || `HTTP ${response.status}`, result.detail].filter(Boolean).join(' ');
            if (!result.retryable || attempt === 2 || stopped) throw Error(message);
            const seconds = Math.max(1, Math.min(60, Number(result.retryAfter) || 10)) * (attempt + 1);
            $('ocrProgress').textContent = `Trang ${job.next} · ${message} Chờ ${seconds} giây, thử lại ${attempt + 1}/2.`;
            await new Promise(resolve => {
                const timer = setTimeout(resolve, seconds * 1000);
                wakeWait = () => { clearTimeout(timer); resolve(); };
            });
            wakeWait = null;
        }
    }

    async function runGemini(from, to, resume) {
        if (busy) return;
        if (!Number.isInteger(from) || !Number.isInteger(to) || from < 1 || to < from) {
            $('ocrProgress').textContent = 'Nhập khoảng trang hợp lệ.'; return;
        }
        if (to - from + 1 > 50) { $('ocrProgress').textContent = 'Tool giới hạn 50 trang mỗi lượt. Hãy chia nhỏ khoảng trang.'; return; }
        if (resume && (!job || job.signature !== signature(from, to))) {
            $('ocrProgress').textContent = 'Nguồn, ngôn ngữ hoặc bố cục đã đổi. Chọn lại cấu hình cũ để tiếp tục, hoặc bắt đầu lượt mới.'; return;
        }
        busy = true;
        stopped = false;
        const previousDisabled = lockedIds.map(id => [id, $(id).disabled]);
        for (const [id] of previousDisabled) $(id).disabled = true;
        $('ocrRun').disabled = $('ocrRange').disabled = true;
        $('ocrStop').hidden = false;
        $('geminiResume').hidden = true;
        let source = null;
        try {
            $('ocrProgress').textContent = 'Đang mở nguồn OCR…';
            source = await window.openOCRSource();
            if (to > source.count) throw Error(`Tài liệu chỉ có ${source.count} trang.`);
            if (!resume) {
                job = {from, to, next: from, model: $('geminiModel').value, language: $('ocrLang').value,
                    layout: $('ocrLayout').value, signature: signature(from, to), name: source.name};
                $('ocrText').value = '';
                geminiOutput = true;
            }
            job.model = $('geminiModel').value;
            while (job.next <= to && !stopped) {
                $('ocrProgress').textContent = `Gemini · trang ${job.next} · hoàn tất ${job.next - from}/${to - from + 1} trang.`;
                const canvas = await source.render(job.next);
                let text;
                try { text = await sendPage(canvas); }
                finally { canvas.width = canvas.height = 0; }
                if (text === null) break;
                if (typeof text !== 'string' || !text.trim()) throw Error('Server trả OCR rỗng. Trang chưa được đánh dấu hoàn tất.');
                $('ocrText').value += ($('ocrText').value ? '\n\n' : '') + `===== PDF ${job.next} =====\n` + text;
                $('ocrOrigin').textContent = `${job.name} · PDF ${from}–${job.next} · model trang gần nhất ${job.model} · ${job.language}`;
                job.next++;
            }
            $('ocrProgress').textContent = `${job.next > to ? 'Hoàn tất' : 'Đã dừng'} · ${job.next - from}/${to - from + 1} trang.${job.lastSeconds ? ' Request cuối mất ' + job.lastSeconds + ' giây.' : ''} Kết quả OCR thô cần đối chiếu.`;
        } catch (error) {
            $('ocrProgress').textContent = `${job ? 'Trang ' + job.next + ' · ' : ''}${error.message} Kết quả đã nhận vẫn được giữ.`;
        } finally {
            if (source) await source.close().catch(() => {});
            for (const [id, disabled] of previousDisabled) $(id).disabled = disabled;
            $('ocrRun').disabled = $('ocrRange').disabled = false;
            $('ocrStop').hidden = true;
            $('geminiResume').hidden = !job || job.next > job.to;
            if (job) $('geminiResume').textContent = `Tiếp tục từ trang ${job.next} đến ${job.to}`;
            busy = false;
        }
    }

    async function dispatch(handler, range) {
        if (busy) return;
        if ($('ocrEngine').value === 'gemini') {
            const from = range ? Number($('ocrFrom').value) : window.BookViewer.current().page;
            const to = range ? Number($('ocrTo').value) : from;
            await runGemini(from, to, false);
            return;
        }
        busy = true;
        geminiOutput = false;
        $('geminiResume').hidden = true;
        job = null;
        $('ocrEngine').disabled = true;
        $('ocrRun').disabled = $('ocrRange').disabled = true;
        try { await handler(); }
        finally {
            busy = false;
            $('ocrEngine').disabled = false;
            $('ocrRun').disabled = $('ocrRange').disabled = false;
        }
    }
    $('ocrRun').onclick = () => dispatch(originalRun, false);
    $('ocrRange').onclick = () => dispatch(originalRange, true);
    $('ocrStop').onclick = () => {
        if ($('ocrEngine').value !== 'gemini') { originalStop(); return; }
        stopped = true;
        if (wakeWait) wakeWait();
        $('ocrProgress').textContent = 'Đang dừng. Request đã gửi có thể vẫn hoàn tất trên Google, sẽ giữ kết quả nếu nhận được.';
    };
    $('geminiResume').onclick = () => { if (job) return runGemini(job.from, job.to, true); };
    const originalOld = $('oldResult').onclick;
    $('oldResult').onclick = async () => {
        if (busy) return;
        job = null;
        geminiOutput = false;
        $('geminiResume').hidden = true;
        await originalOld();
    };
    $('ocrDownload').onclick = () => {
        if (!geminiOutput) { originalDownload(); return; }
        const link = document.createElement('a');
        const url = URL.createObjectURL(new Blob([$('ocrText').value], {type: 'text/plain;charset=utf-8'}));
        link.href = url;
        link.download = `gemini_ocr_${job.from}-${Math.max(job.from, job.next - 1)}_chua_sua.txt`;
        link.click();
        setTimeout(() => URL.revokeObjectURL(url), 1000);
    };
})();
