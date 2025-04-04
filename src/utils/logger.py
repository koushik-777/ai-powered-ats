class Logger:
    def __init__(self, log_file='application.log'):
        self.log_file = log_file

    def log(self, message):
        with open(self.log_file, 'a') as file:
            file.write(f"{self._get_timestamp()} - {message}\n")

    def _get_timestamp(self):
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def log_error(self, error_message):
        self.log(f"ERROR: {error_message}")

    def log_info(self, info_message):
        self.log(f"INFO: {info_message}")