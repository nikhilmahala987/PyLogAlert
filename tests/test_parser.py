from core.parser import parse_log_line

def test_sshd_log_parses_correctly():
    log_line = "Sep 1 10:00:02 main-server sshd[1234]: Failed password for root from 185.191.171.13 port 44326 ssh2"
    parsed_result = parse_log_line(log_line)
    assert parsed_result is not None
    assert parsed_result['hostname'] == 'main-server'
    assert parsed_result['process_name'] == 'sshd'
    assert parsed_result['pid'] == '1234'
    assert parsed_result['source_ip'] == '185.191.171.13'
def test_unrelated_log_returns_none():
    log_line = "Sep 1 10:00:01 firewall UFW BLOCK IN=eth0 OUT= MAC=01:02:03:04:05:06"
    parsed_result = parse_log_line(log_line)
    assert parsed_result is None