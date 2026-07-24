"""Custom_Widgets.Utils.download_font — remote font loading (mocked network).

Covers: successful download writes + caches a file, a second call re-uses the
cache without hitting the network, and any failure is non-fatal (returns None)
so the app falls back to the bundled font."""

import io
from contextlib import contextmanager
from unittest import mock


@contextmanager
def _fake_urlopen(payload):
    calls = {"n": 0}

    def _open(req, timeout=None):
        calls["n"] += 1
        return io.BytesIO(payload)

    with mock.patch("urllib.request.urlopen", side_effect=_open):
        yield calls


def test_download_and_cache(tmp_path):
    from Custom_Widgets.Utils import download_font
    url = "https://example.com/fonts/Demo-Regular.ttf"
    payload = b"\x00\x01\x00\x00fake-ttf-bytes"
    with _fake_urlopen(payload) as calls:
        p1 = download_font(url, cache_dir=str(tmp_path))
        assert p1 and p1.endswith(".ttf")
        with open(p1, "rb") as f:
            assert f.read() == payload
        # second call is served from cache — no extra network hit
        p2 = download_font(url, cache_dir=str(tmp_path))
        assert p2 == p1
        assert calls["n"] == 1


def test_unknown_extension_defaults_to_ttf(tmp_path):
    from Custom_Widgets.Utils import download_font
    with _fake_urlopen(b"data"):
        p = download_font("https://x/y/font-with-no-ext", cache_dir=str(tmp_path))
        assert p and p.endswith(".ttf")


def test_failure_is_non_fatal(tmp_path):
    from Custom_Widgets.Utils import download_font

    def _boom(req, timeout=None):
        raise OSError("network down")

    with mock.patch("urllib.request.urlopen", side_effect=_boom):
        assert download_font("https://x/y.ttf", cache_dir=str(tmp_path)) is None
