# sqli_tool/analyzer.py

class ResponseInfo:
    def __init__(self, response):
        if response is None:
            self.status = 0
            self.length = 0
            self.text = ""
        else:
            self.status = response.status_code
            self.length = len(response.text)
            self.text = response.text

def is_vulnerable(r_base, r_test):
    """
    Intelligently compares a baseline response to a test response.
    Returns True if there is a significant difference.
    """
    if r_base.status == 0 or r_test.status == 0:
        return False
        
    # Difference in status code is a clear signal
    if r_base.status != r_test.status:
        return True
    
    # Significant length difference (more than 5 bytes)
    if abs(r_base.length - r_test.length) > 5:
        return True
    
    return False

def analyze_time(start_time, end_time, threshold=4):
    """
    Checks if the response took longer than the specified threshold.
    """
    return (end_time - start_time) > threshold
