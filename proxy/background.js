var config = {
  mode: "fixed_servers",
  rules: {
    singleProxy: {
      scheme: "http",
      host: "代理主机名",
      port: 端口
    },
    bypassList: ["不通过代理的地址"]
  }
};

chrome.proxy.settings.set({
  value: config,
  scope: "regular"
}, function () {});

function callbackFn(details) {
  return {
    authCredentials: {
      username: '用户名',
      password: "密码"
    }
  };
}

chrome.webRequest.onAuthRequired.addListener(
  callbackFn, {
    urls: ["<all_urls>"]
  },
  ['blocking']
);