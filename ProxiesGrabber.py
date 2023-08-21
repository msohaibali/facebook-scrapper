import requests


class ProxiesGrabber:
    @staticmethod
    def build_proxies_list(
        proxies_list: list,
        dict_proxy: bool = True,
    ) -> list:
        parsed_proxies_list = list()
        if dict_proxy:
            for single_item in proxies_list:
                proxy_dict = {
                    "http": "http://{USERNAME}:{PASSWORD}@{IP}:{PORT}/".format(
                        USERNAME=single_item.get("username"),
                        PASSWORD=single_item.get("password"),
                        IP=single_item.get("proxy_address"),
                        PORT=single_item.get("port"),
                    )
                }
                parsed_proxies_list.append(proxy_dict)
        else:
            for single_item in proxies_list:
                proxy_str = "{USERNAME}:{PASSWORD}@{IP}:{PORT}".format(
                    USERNAME=single_item.get("username"),
                    PASSWORD=single_item.get("password"),
                    IP=single_item.get("proxy_address"),
                    PORT=single_item.get("port"),
                )
                parsed_proxies_list.append(proxy_str)

        return parsed_proxies_list

    @staticmethod
    def get_proxies_list(
        token: str,
        proxies_url: str,
    ) -> list:
        headers = {"Authorization": "Token " + token}

        proxies_response = requests.get(
            proxies_url,
            headers=headers,
        )

        if proxies_response.ok:
            proxies_response = proxies_response.json()
            results = proxies_response.get("results")
            proxies_list = ProxiesGrabber.build_proxies_list(results)
            return proxies_list

        else:
            print("[-]  Issue in Proxies Request")
            return []


# ProxiesGrabber.get_proxies_list(
#     token="z1d912p9wgzakaivpw3cvjf9fds8vd6dqanwwksh",
#     proxies_url="https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100",
# )
