from orders.wsgi import *
from datetime import datetime
from orders.settings import BASE_DIR
from web_service.models import ProductInfo
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = ProductInfo

    def export_from_db(self):
        dataset = ProductResource().export()
        data_csv = dataset.csv

        return data_csv

    def write_txt_file(self):
        data_csv = ProductResource.export_from_db(ProductResource)
        export_folder = f"{BASE_DIR}/import_export_goods/export_files/"
        with open(f"{export_folder}export_goods_{str(datetime.now())[:-7]}.txt", "w",
                  encoding="utf-8") as file:
            file.write(str(data_csv))


if __name__ == "__main__":
    exp_obj = ProductResource()
    exp_obj.export_from_db()
    exp_obj.write_txt_file()
