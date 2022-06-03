class PostRequests:

    @staticmethod
    def input_data_analysis(data):
        result_dict = {}
        if data:
            params = data.split('&')
            for param in params:
                key, value = param.split('=')
                result_dict[key] = value
        return result_dict

    @staticmethod
    def receive_wsgi_data(env) -> bytes:
        content_length_data = env.get('CONTENT_LENGTH')

        if content_length_data:
            content_length = int(content_length_data)
        else:
            content_length = 0

        print(content_length)

        if content_length > 0:
            data = env['wsgi.input'].read(content_length)
        else:
            data = b''

        return data

    def wsgi_input_data_analysis(self, data) -> dict:
        result_dict = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            print(data_str)
            result_dict = self.input_data_analysis(data_str)
        return result_dict

    def get_request_params(self, env):
        data = self.receive_wsgi_data(env)
        data = self.wsgi_input_data_analysis(data)
        return data


class GetRequests:

    @staticmethod
    def input_data_analysis(data: str):
        result_dict = {}
        if data:
            params = data.split('&')
            for param in params:
                key, value = param.split('=')
                result_dict[key] = value
        return result_dict

    @staticmethod
    def get_request_params(env):
        query_string = env['QUERY_STRING']
        request_params = GetRequests.input_data_analysis(query_string)
        return request_params
