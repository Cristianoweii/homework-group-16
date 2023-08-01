  "manifest_version": 2,
  "name": "Your Password Manager",
  "version": "1.0",
  "description": "A password manager extension for Google Chrome",
  "permissions": [
    "tabs",
    "storage"
  ],
  "content_scripts": [
    {
      "matches": ["<all_urls>"],
      "js": ["content.js"]
    }
  ],
  "browser_action": {
    "default_icon": "icon.png",
    "default_popup": "popup.html"
  }

