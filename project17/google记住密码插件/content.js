// 监听登录表单的提交事件
document.addEventListener("submit", function(event) {
  const form = event.target;
  const username = form.querySelector("input[type='text']").value;
  const password = form.querySelector("input[type='password']").value;
  const site = window.location.href;

  // 将用户名和密码保存到本地存储
  chrome.storage.local.get("passwords", function(data) {
    const passwords = data.passwords || {};
    passwords[site] = password;
    chrome.storage.local.set({ "passwords": passwords });
  });
});
