def info(func):
    def wrapper(self, *args, **options):
        if self.CLS.objects.exists():
            self.stdout.write(
                f'{self.FILE_NAME} data already loaded...exiting.')
            return
        self.stdout.write(f'Loading {self.FILE_NAME} data')
        func(self, *args, **options)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully loaded: {self.CLS.objects.all()}'))
    return wrapper
