// 从本地存储中获取保存的密码列表
chrome.storage.local.get("passwords", function(data) {
  const passwordList = document.getElementById("passwordList");

  // 显示密码列表
  if (data.passwords) {
    for (const site in data.passwords) {
      const passwordEntry = data.passwords[site];
      const listItem = document.createElement("li");
      listItem.textContent = `Site: ${site}, Password: ${passwordEntry}`;
      passwordList.appendChild(listItem);
    }
  }
});
