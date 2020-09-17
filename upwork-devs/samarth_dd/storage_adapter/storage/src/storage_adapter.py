import logging

class BaseStorageAdapter(object):
    """
    This is an abstract class that represents the interface
    that all storage adapters should implement.
    """
    def __init__(self, *args, **kwargs):

            """
            Initialize common attributes shared by all storage adapters.
            :param str tagger_language: The language that the tagger uses to remove stopwords.
            """
            self.logger = kwargs.get('logger', logging.getLogger(__name__))

    def bucket_exists(self,bucket_name):
        """
               Check bucket with given bucket name exists.
               bucket_name is case insensitive.
        """

        raise self.AdapterMethodNotImplementedError(
            'The `create_bucket` method is not implemented by this adapter.'
        )


    def create_bucket(self,bucket_name):
             """
               Creates bucket with given bucket name.
               bucket_name is case insensitive.
             """

             raise self.AdapterMethodNotImplementedError(
                'The `create_bucket` method is not implemented by this adapter.'
             )

    def remove_bucket(self,bucket_name):
         """
           deletes bucket with given bucket name.
           bucket_name is case insensitive.
         """

         raise self.AdapterMethodNotImplementedError(
             'The `remove_bucket` method is not implemented by this adapter.'
         )

    def remove_file(self,bucket_name,file_name):
        """
        Drop the database attached to a given adapter.
        """
        raise self.AdapterMethodNotImplementedError(
            'The `remove_file` method is not implemented by this adapter.'
        )

    def get_bucket_list(self):
        """
            lists all  buckets.
        """
        get_bucket_list=[]
        return get_bucket_list

    def get_all_files(self,bucket_name):
        """
            lists all  files for given bucket_name.
        """
        get_file_list = []
        return get_file_list

    def upload_file(self,bucket_name,file_name,file_path):
        """
            uploads file mentioned in file_path to bucket specified by bucket_name with name as given file_name
        """

    def upload_data_stream(self,bucket_name,file_name,data_stream,data_type):
        """
            uploads data stream directly to given bucket_name
        """

    def download_all_files(self,bucket_name,download_path):
        """
            downloads all files inside bucket specified by bucket_name to specified path
        """

    def download_n_files(self,bucket_name,download_path, num_of_files):
        """
            downloads n number of files inside bucket specified by bucket_name to specified path
        """

    def set_policy(self,bucket_name,policy):
        """
            you can set policy to specific bucket
        """
        raise self.AdapterMethodNotImplementedError(
            'The `set_policy` method is not implemented by this adapter.'
        )

    def get_policy(self, bucket_name):
        """
            you can get policy to specific bucket
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_policy` method is not implemented by this adapter.'
        )

    def get_meta_data(self,bucket_name,file_name):
        """
            get meta_data of bucket
        """
        raise self.AdapterMethodNotImplementedError(
            'The `get_meta_data` method is not implemented by this adapter.'
        )

    def count_files(self,bucket_name):
        """
            count number of files of bucket
        """

        raise self.AdapterMethodNotImplementedError(
            'The `count` method is not implemented by this adapter.'
        )

    class AdapterMethodNotImplementedError(NotImplementedError):
        """
        An exception to be raised when a storage adapter method has not been implemented.
        Typically this indicates that the method should be implement in a subclass.
        """
        pass
