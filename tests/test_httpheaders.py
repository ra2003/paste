from paste.httpheaders import *

def test_sorting():
    # verify the HTTP_HEADERS are set with their canonical form
    sample = [HTTP_WWW_AUTHENTICATE, HTTP_VIA, HTTP_ACCEPT, HTTP_DATE,
    HTTP_ACCEPT_CHARSET, HTTP_AGE, HTTP_ALLOW, HTTP_CACHE_CONTROL,
    HTTP_CONTENT_ENCODING, HTTP_ETAG, HTTP_CONTENT_TYPE, HTTP_FROM,
    HTTP_EXPIRES, HTTP_RANGE, HTTP_UPGRADE, HTTP_VARY, HTTP_ALLOW]
    sample.sort()
    sample = [(x.category, str(x)) for x in sample]
    assert sample == [
     # general headers first
     ('general', 'Cache-Control'),
     ('general', 'Date'),
     ('general', 'Upgrade'),
     ('general', 'Via'),
     # request and response
     ('request', 'Accept'),
     ('request', 'Accept-Charset'),
     ('response', 'Age'),
     ('response', 'ETag'), # ETag is odd case
     ('request', 'From'),
     ('request', 'Range'),
     ('response', 'Vary'),
     ('response', 'WWW-Authenticate'), # so is WWW-Authenticate
     # entity headers last
     ('entity', 'Allow'), # expected duplicate
     ('entity', 'Allow'),
     ('entity', 'Content-Encoding'),
     ('entity', 'Content-Type'),
     ('entity', 'Expires')]

def test_normalize():
    response_headers = [
       ('www-authenticate','Response AuthMessage'),
       ('unknown-header','Unknown Sorted Last'),
       ('Via','General Bingles'),
       ('aLLoW','Entity Allow Something'),
       ('ETAG','Response 34234'),
       ('expires','Entity An-Expiration-Date'),
       ('date','General A-Date')]
    normalize_headers(response_headers, strict=False)
    assert response_headers == [
     ('Date', 'General A-Date'),
     ('Via', 'General Bingles'),
     ('ETag', 'Response 34234'),
     ('WWW-Authenticate', 'Response AuthMessage'),
     ('Allow', 'Entity Allow Something'),
     ('Expires', 'Entity An-Expiration-Date'),
     ('Unknown-Header', 'Unknown Sorted Last')]
