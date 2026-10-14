"""Read-only demo login for the public live demo.

Visitors sign in as DEMO_USERNAME / DEMO_PASSWORD (settings, from the environment). The demo employee can open
every page, but any save or delete (a non-GET request) is refused, and each page shows a small banner. The demo
account is created on the first request if it does not exist.
"""
from django.conf import settings
from django.http import HttpResponseRedirect

from employees.models import Employee

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")
OPEN_PATHS = ("/login/", "/logout/")
BANNER = (
    '<div style="position:sticky;top:0;z-index:9999;background:#fff3cd;color:#664d03;padding:8px 16px;'
    'font:14px/1.4 system-ui,sans-serif;text-align:center;border-bottom:1px solid #ffe69c">'
    "Demo mode: look around freely; changes are not saved. "
    '<a href="/logout/" style="color:#664d03;font-weight:600">Log out</a></div>'
)


def demo_username():
    return getattr(settings, "DEMO_USERNAME", "") or ""


class DemoReadOnlyMiddleware:
    _ensured = False

    def __init__(self, get_response):
        self.get_response = get_response

    def _ensure_demo_account(self):
        if DemoReadOnlyMiddleware._ensured or not demo_username():
            return
        if not Employee.objects.filter(username=demo_username()).exists():
            Employee(name="Demo Visitor", age=30, phone="000 000 000", address="Phnom Penh",
                     username=demo_username(), password=settings.DEMO_PASSWORD).save()
        DemoReadOnlyMiddleware._ensured = True

    def _is_demo(self, request):
        employee_id = request.session.get("employee_id")
        if not employee_id or not demo_username():
            return False
        if request.session.get("demo_for") != employee_id:
            request.session["demo_for"] = employee_id
            request.session["is_demo"] = Employee.objects.filter(
                id=employee_id, username=demo_username()).exists()
        return bool(request.session.get("is_demo"))

    def __call__(self, request):
        self._ensure_demo_account()
        demo = self._is_demo(request)
        if demo and request.method not in SAFE_METHODS and request.path not in OPEN_PATHS:
            return HttpResponseRedirect(request.META.get("HTTP_REFERER") or "/")
        response = self.get_response(request)
        if demo and response.get("Content-Type", "").startswith("text/html") and not response.streaming:
            charset = response.charset or "utf-8"
            html = response.content.decode(charset)
            start = html.find("<body")
            if start != -1:
                end = html.find(">", start) + 1
                response.content = (html[:end] + BANNER + html[end:]).encode(charset)
                if response.has_header("Content-Length"):
                    response["Content-Length"] = str(len(response.content))
        return response
