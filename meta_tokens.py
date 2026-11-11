"""Read-only Meta requests with complete-page fallback across configured tokens."""
import requests
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

class MetaTokenClient:
    def __init__(self, tokens):
        self.tokens = dict(tokens)

    def _request(self, url, params, token, timeout):
        # Pagination URLs can contain the previous credential: replace it explicitly.
        parts = urlsplit(url)
        query = [(k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True) if k != 'access_token']
        clean_url = urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
        args = dict(params or {})
        args['access_token'] = token
        response = requests.get(clean_url, params=args, timeout=timeout)
        response.raise_for_status()
        data = response.json()
        if 'error' in data:
            raise RuntimeError(str(data['error']))
        return data

    def _run(self, url, params, token_key, paginate, timeout):
        candidates = [(token_key, self.tokens[token_key])] if token_key else list(self.tokens.items())
        errors = []
        for key, token in candidates:
            try:
                current_url, current_params = url, params
                rows = []
                while True:
                    data = self._request(current_url, current_params, token, timeout)
                    if not paginate:
                        return data
                    rows.extend(data.get('data', []))
                    current_url = data.get('paging', {}).get('next')
                    if not current_url:
                        return rows
                    current_params = None
            except Exception as exc:
                message = str(exc)
                for secret in self.tokens.values():
                    message = message.replace(secret, '[REDACTED]')
                errors.append(f'{key}: {message}')
        raise RuntimeError('Meta request failed: ' + ' | '.join(errors))

    def fetch_all_pages(self, url, params=None, token_key=None):
        return self._run(url, params, token_key, True, 90)

    def get_object(self, url, params=None, timeout=90):
        return self._run(url, params, None, False, timeout)
