
def test_http_status(request, expected_status):
    r = {
        'text': "HTTP status code is %s " % (expected_status),
        'success': False,
        'error': ''
    }

    r['success'] = request.status_code == expected_status
    if not r['success']:
        r['error'] = "HTTP status code is not %s (got: %s) " % (expected_status, request.status_code)

    return r


def test_header(request, name, value=None):
    r = {
        'text': "header %s contains %s " % (name, value),
        'success': False,
        'error': ''
    }

    if value is None:
        r['text'] = "header %s exists" % (name)

    try:
        header = request.headers[name]
    except Exception as e:
        header = False
        r['error'] = "Header %s not among request headers " % (name)

    if header:
        if value:
            r['success'] = value.lower() in header.lower()
            if not r['success']:
                r['error'] = "Header %s does not contain %s (got: %s)" % (name, value, header)

        else:
            # I only need to check if the header exists
            r['success'] = True

    return r
