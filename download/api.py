from zope import component

from download.downloader import DatasetDownloader, DataSetForServiceDownloader, DataServiceDownloader
from download.interfaces import IDatasetDownloader, IDataserviceDownloader, IDatasetForServiceDownloader


def get_dataset_downloader():
    comp = component.queryUtility(IDatasetDownloader)
    if comp is None:
        d = DatasetDownloader()
        register_dataset_downloader(d)
        return d
    else:
        return comp


def unregister_dataset_downloader():
    component.provideUtility(None, IDatasetDownloader)


def register_dataset_downloader(downloader):
    component.provideUtility(downloader, IDatasetDownloader)


def get_dataservice_downloader():
    comp = component.queryUtility(IDataserviceDownloader)
    if comp is None:
        d = DataServiceDownloader()
        register_dataservice_downloader(d)
        return d
    else:
        return comp


def unregister_dataservice_downloader():
    component.provideUtility(None, IDataserviceDownloader)


def register_dataservice_downloader(downloader):
    component.provideUtility(downloader, IDataserviceDownloader)


def get_dataset_for_service_downloader():
    comp = component.queryUtility(IDatasetForServiceDownloader)
    if comp is None:
        d = DataSetForServiceDownloader()
        register_dataset_for_service_downloader(d)
        return d
    else:
        return comp


def unregister_dataset_for_service_downloader():
    component.provideUtility(None, IDatasetForServiceDownloader)


def register_dataset_for_service_downloader(downloader):
    component.provideUtility(downloader, IDatasetForServiceDownloader)


def run_downloader(uris, graph=None):
    # this is just the mime type for collecting data
    mime_type = 'text/turtle'
    datasets = get_dataset_downloader()
    datasets.run(uris, mime_type, graph=graph)

    dataservices = get_dataservice_downloader()
    dataservices.run(uris, mime_type, graph=graph)

    datasets_for_service = get_dataset_for_service_downloader()
    datasets_for_service.run(uris, mime_type, graph=graph)