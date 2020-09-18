from datetime import datetime
from datetime import datetime
from unittest import TestCase, mock

import pytz
from gw_crawler.malicious_file_crawler.test.responses.minio_mocks import MockConnection, MockResponse
from minio.api import _DEFAULT_USER_AGENT
from minio.error import InvalidBucketError, NoSuchBucket
from nose.tools import eq_, raises
from requests.cookies import MockResponse
from storage.src.adapter_object_creator import ObjectCreator
from storage.src.minio_adapter import MinioAdapter
from twisted.conch.test.test_channel import MockConnection


class TestMinioAdapter(TestCase):

    def setUp(self):
        self.adapter = ObjectCreator.get_storage_adapter(self)

    @raises(TypeError)
    def test_bucket_is_string(self):
        self.adapter.create_bucket(1234)

    @raises(InvalidBucketError)
    def test_bucket_is_not_empty_string(self):
        self.adapter.create_bucket('  \t \n  ')

    @raises(InvalidBucketError)
    def test_bucket_exists_invalid_name(self):
        self.adapter.create_bucket('AB*CD')

    @mock.patch('urllib3.PoolManager')
    def test_make_bucket_works(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('PUT',
                         'https://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}

        service = MinioAdapter(config)

    @mock.patch('urllib3.PoolManager')
    def test_empty_list_buckets_works(self, mock_connection):
        mock_data = ('<ListAllMyBucketsResult '
                     'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                     '<Buckets></Buckets><Owner><ID>minio</ID><DisplayName>'
                     'minio</DisplayName></Owner></ListAllMyBucketsResult>')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('GET', 'http://localhost:9000/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200, content=mock_data)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        buckets = service.get_bucket_list()
        count = 0
        for bucket in buckets:
            count += 1
        eq_(0, count)

    @mock.patch('urllib3.PoolManager')
    def test_list_buckets_works(self, mock_connection):
        mock_data = ('<ListAllMyBucketsResult '
                     'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                     '<Buckets><Bucket><Name>hello</Name>'
                     '<CreationDate>2015-06-22T23:07:43.240Z</CreationDate>'
                     '</Bucket><Bucket><Name>world</Name>'
                     '<CreationDate>2015-06-22T23:07:56.766Z</CreationDate>'
                     '</Bucket></Buckets><Owner><ID>minio</ID>'
                     '<DisplayName>minio</DisplayName></Owner>'
                     '</ListAllMyBucketsResult>')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('GET', 'http://localhost:9000/',
                         {'User-Agent': _DEFAULT_USER_AGENT},
                         200, content=mock_data)
        )

        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        buckets = service.get_bucket_list()
        buckets_list = []
        count = 0
        for bucket in buckets:
            count += 1
            buckets_list.append(bucket)
        eq_(2, count)
        eq_('hello', buckets_list[0].name)
        eq_(datetime(2015, 6, 22, 23, 7, 43, 240000,
                     pytz.utc), buckets_list[0].creation_date)
        eq_('world', buckets_list[1].name)
        eq_(datetime(2015, 6, 22, 23, 7, 56, 766000,
                     pytz.utc), buckets_list[1].creation_date)

    @raises(TypeError)
    def test_bucket_is_string(self):
        self.adapter.remove_bucket(1234)

    @raises(InvalidBucketError)
    def test_bucket_is_not_empty_string(self):
        self.adapter.remove_bucket('  \t \n  ')

    @raises(InvalidBucketError)
    def test_remove_bucket_invalid_name(self):
        self.adapter.remove_bucket('AB*CD')

    @mock.patch('urllib3.PoolManager')
    def test_remove_bucket_works(self, mock_connection):

        mock_data = ('<ListAllMyBucketsResult '
                     'xmlns="http://s3.amazonaws.com/doc/2006-03-01/">'
                     '<Buckets><Bucket><Name>hello</Name>'
                     '<CreationDate>2015-06-22T23:07:43.240Z</CreationDate>'
                     '</Bucket><Bucket><Name>world</Name>'
                     '<CreationDate>2015-06-22T23:07:56.766Z</CreationDate>'
                     '</Bucket></Buckets><Owner><ID>minio</ID>'
                     '<DisplayName>minio</DisplayName></Owner>'
                     '</ListAllMyBucketsResult>')
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        mock_server.mock_add_request(
            MockResponse('DELETE',
                         'https://localhost:9000/hello/',
                         {'User-Agent': _DEFAULT_USER_AGENT}, 204)
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None}
        service = MinioAdapter(config)
        service.remove_bucket('hello')

    @raises(InvalidBucketError)
    def test_object_is_string(self):
        self.adapter.remove_file('hello', 1234)

    @raises(InvalidBucketError)
    def test_object_is_not_empty_string(self):
        self.adapter.remove_file('hello', '  \t \n  ')

    @mock.patch('urllib3.PoolManager')
    @raises(NoSuchBucket)
    def test_get_policy_for_non_existent_bucket(self, mock_connection):
        mock_server = MockConnection()
        mock_connection.return_value = mock_server
        bucket_name = 'non-existent-bucket'
        mock_server.mock_add_request(
            MockResponse(
                'GET',
                'https://localhost:9000/' + bucket_name + '/?policy=',
                {'User-Agent': _DEFAULT_USER_AGENT},
                404,
            )
        )
        config = {'HOSTNAME': 'localhost:9000', "AWS_ACCESS_KEY_ID": None, 'AWS_SECRET_ACCESS_KEY': None,
                  'SECURE': True}
        service = MinioAdapter(config)
        service.get_policy(bucket_name)
