import { expect, test } from "bun:test";
import { spawnSync } from "node:child_process";

const script = `
import json
from unittest.mock import patch
import nextsms

results = {}

def check(name, fn):
    try:
        fn()
        results[name] = "ok"
    except Exception as exc:
        results[name] = type(exc).__name__ + ": " + str(exc)

class Resp:
    def __init__(self, code, body=None, redirect=False):
        self.status_code = code
        self.is_redirect = redirect
        self._body = {} if body is None else body
    def json(self):
        return self._body

def test_sandbox():
    c = nextsms("user", "s3cr3t-test", sandbox=True)
    assert c.sandbox is True
    assert c.base_url_single.endswith("/test/text/single")
    c.sandbox = False
    assert c.sandbox is False
    assert "/test/" not in c.base_url_single

def test_password_hidden():
    c = nextsms("user", "s3cr3t-test")
    text = repr(c) + repr(c._user)
    assert "s3cr3t-test" not in text
    assert "s3cr3t-test" not in c.create_header()["Authorization"]

def test_empty_login():
    try:
        nextsms("user", "")
    except ValueError:
        return
    raise AssertionError("empty password was accepted")

def test_bad_phone():
    c = nextsms("user", "s3cr3t-test", sandbox=True)
    with patch("requests.post") as post:
        try:
            c.sendsms("hello", "255700000000,255711111111", "NEXTSMS")
        except ValueError:
            assert post.call_count == 0
            return
        raise AssertionError("bad phone was accepted")

def test_bulk_extra_field():
    c = nextsms("user", "s3cr3t-test", sandbox=True)
    with patch("requests.post") as post:
        try:
            c.send_bulk([{
                "from": "NEXTSMS",
                "to": "255700000000",
                "text": "hi",
                "callback": "https://example.test",
            }])
        except ValueError:
            assert post.call_count == 0
            return
        raise AssertionError("extra field was accepted")

def test_send_ok():
    c = nextsms("user", "s3cr3t-test", sandbox=True)
    with patch("requests.post", return_value=Resp(200, {"messages": []})) as post:
        body = c.sendsms("hello", ["255700000000"], "NEXTSMS")
        assert body == {"messages": []}
        kwargs = post.call_args.kwargs
        assert kwargs["allow_redirects"] is False
        assert kwargs["verify"] is True
        assert kwargs["timeout"] == 10
        assert post.call_args.args[0].startswith("https://messaging-service.co.tz/")

def test_http_error():
    c = nextsms("user", "s3cr3t-test", sandbox=True)
    with patch("requests.post", return_value=Resp(401)):
        try:
            c.sendsms("hello", "255700000000", "NEXTSMS")
        except nextsms.Error as exc:
            assert exc.status_code == 401
            assert "s3cr3t-test" not in str(exc)
            return
        raise AssertionError("401 was treated as success")

def test_redirect():
    c = nextsms("user", "s3cr3t-test", sandbox=True)
    with patch("requests.post", return_value=Resp(302, redirect=True)):
        try:
            c.sendsms("hello", "255700000000", "NEXTSMS")
        except nextsms.Error as exc:
            assert exc.status_code == 302
            return
        raise AssertionError("redirect was followed")

def test_url_swap():
    nextsms.PRODUCTION_URL_SINGLE = "https://example.test/collect"
    c = nextsms("user", "s3cr3t-test", sandbox=False)
    with patch("requests.post", return_value=Resp(200, {"ok": True})) as post:
        c.sendsms("hello", "255700000000", "NEXTSMS")
        assert post.call_args.args[0] == "https://messaging-service.co.tz/api/sms/v1/text/single"

check("sandbox flag sticks", test_sandbox)
check("password stays out of repr", test_password_hidden)
check("empty login is rejected", test_empty_login)
check("bad phone is rejected", test_bad_phone)
check("bulk extra field is rejected", test_bulk_extra_field)
check("send uses timeout and no redirect", test_send_ok)
check("http error is raised", test_http_error)
check("redirect is not followed", test_redirect)
check("swapped url is ignored", test_url_swap)
print(json.dumps(results))
`;

const ran = spawnSync("python3", ["-c", script], {
  encoding: "utf-8",
  cwd: import.meta.dir,
});

if (ran.status !== 0) {
  throw new Error(ran.stderr || ran.stdout || "python checks failed");
}

const results = JSON.parse(ran.stdout) as Record<string, string>;

for (const name of Object.keys(results)) {
  test(name, () => {
    expect(results[name]).toBe("ok");
  });
}
