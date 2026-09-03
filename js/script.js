// 테마 변경 (다크모드)
document.getElementById('theme-toggle').addEventListener('click', () => {
    document.body.classList.toggle('dark');
});

// AI 호출 및 예외 처리
document.getElementById('chat-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const input = document.getElementById('user-input');
    const result = document.getElementById('result-display');
    const loading = document.getElementById('loading');
    const button = document.getElementById('ask-button');
    const message = input.value.trim();

    if (!message) {
        alert("상황을 입력해주세요! (예: 식당에서)");
        return;
    }

    loading.classList.remove('hidden');
    button.disabled = true;
    result.innerText = "";

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json().catch(() => ({}));
        if (response.ok) {
            result.innerText = data.reply || "응답을 받지 못했습니다.";
        } else {
            result.innerText = "❌ 오류: " + (data.error || "문제가 발생했습니다.");
        }
    } catch {
        result.innerText = "❌ 연결 오류가 발생했습니다. 인터넷을 확인해주세요.";
    } finally {
        loading.classList.add('hidden');
        button.disabled = false;
    }
});