from pydash import _
import requests, feedparser, random
from time import sleep

from src.logger import Logger
from src.constants import Constants

logger = Logger.get_logger()

class Utils:

    def is_include_in_string(include_to_test, string) -> bool:
        if isinstance(include_to_test, str) or isinstance(include_to_test, int):
            return str(include_to_test).upper() in string \
                or str(include_to_test).lower() in string
        else:
            is_include = False
            for to_test_str in include_to_test:
                if str(to_test_str).upper() in string \
                    or str(to_test_str).lower() in string:
                    is_include = True
            return is_include

    def sanitize_check(url, generator_exist) -> bool:
        def try_to_reach():
            is_valid = False
            try:
                feed_data = feedparser.parse(url).entries
                if feed_data == [] and generator_exist:
                    api_gen_url = Constants.api_url + "/create?url=" + url
                    status = Utils.get_request(api_gen_url).status_code
                    is_valid = status == 200
                elif feed_data != []:
                    is_valid = True
            except:
                logger.error(f"An error occured. No answer from host {url}. "
                    + f"Please verify if the submitted URL is valid"
                )
            return is_valid
        is_valid = try_to_reach()
        if not is_valid: # try to reach a second time
            is_valid = try_to_reach()
        return is_valid

    def generate_random_string() -> str:
        random_string = ""
        for _ in range(5):
            random_integer = random.randint(97, 97 + 26 - 1)
            flip_bit = random.randint(0, 1)
            random_integer = random_integer - 32 if flip_bit == 1 else random_integer
            random_string += (chr(random_integer))
        return random_string

    def everyone_tag_is_not_used(message) -> bool:
        return not Utils.is_include_in_string('everyone', message)

    def get_request(url, **options) -> requests.Response:
        extra_cookies = options.pop('cookies', {})
        extra_headers = options.pop('headers', {})
        timeout = options.pop('timeout', 5)
        headers = {
            "User-Agent": Utils.get_user_agent(),
            "Retry-After": "5",
            }
        for key, value in extra_headers.items():
            headers[key] = value
        return requests.get(url, timeout=timeout, headers=headers, cookies=extra_cookies)

    def try_again_if_fail(resolve, max_retry=3, **args) -> None:
        for attempt in range(max_retry):
            try:
                resolve(*args["resolve_args"]) if "resolve_args" in args else resolve()
                break
            except Exception:
                if "reject" in args:
                    args["reject"](Exception, *args["resolve_args"]) if "reject_args" not in args else args["reject"]()
                if attempt < max_retry:
                    retry_delay = 2
                    logger.error(f"Fail, retry in {retry_delay} seconds")
                    sleep(retry_delay)
                resolve(*args["resolve_args"]) if "resolve_args" in args else resolve()

    def get_user_agent(reddit_username: str = None):
        reddit_msg = "" if reddit_username is None else f"My Reddit account is u/{reddit_username}" 
        return (f"Mozilla/5.0 - {reddit_msg} This is a bot from this project {Constants.source_code_url}."
            + "Please do not ban me. It has been build to help following updates from feeds."
            + f"The purpose is only to gather informations every {Constants.base_config_default['refresh_time']} seconds."
            + f"This is an fully open-source project")
