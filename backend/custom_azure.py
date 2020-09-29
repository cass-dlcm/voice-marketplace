from storages.backends.azure_storage import AzureStorage
import yaml


class AzureMediaStorage(AzureStorage):
    account_name = 'voicemarketrecordings'  # Must be replaced by your storage_account_name
    account_key = yaml.load(open('secrets.yaml'), Loader=yaml.FullLoader)['storage_account_key']  # Must be replaced by your <storage_account_key>
    azure_container = 'media'
    expiration_secs = None


class AzureStaticStorage(AzureStorage):
    account_name = 'voicemarketrecordings'  # Must be replaced by your storage_account_name
    account_key = yaml.load(open('secrets.yaml'), Loader=yaml.FullLoader)['storage_account_key']  # Must be replaced by your <storage_account_key>
    azure_container = 'static'
    expiration_secs = None
