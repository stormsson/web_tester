

def test_contains(driver, selector, value=None):

    r = {
        'text': "%s contains %s " % (selector, value),
        'success': False,
        'error': ''
    }

    if value is None:
        r['text'] = "%s exists " % ( selector )

    try:
        element = driver.find_element_by_css_selector(selector)
    except Exception as e:
        element = False
        r['error'] = str(e)
        pass

    if element:
        if value:
            r['success'] = value.lower() in element.text.lower()
        else:
            # I only need to check if the element exists
            r['success'] = True

        if not r['success']:
            r['error'] = "Element %s does not contain %s " % (selector, value)

    return r