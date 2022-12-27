from orders.wsgi import *
from datetime import datetime
from orders.settings import BASE_DIR
from web_service.models import ProductInfo, Product
from import_export import resources


class ProductResource(resources.ModelResource):
    class Meta:
        model = ProductInfo

    def export_from_db(self):
        dataset = ProductResource().export()
        data_csv = dataset.csv
        data_dict = dataset.dict
        data_json = dataset.get_json()

        return data_csv, data_dict, data_json

    def write_file(self):
        data_csv, data_dict, data_json = ProductResource.export_from_db(ProductResource)
        export_folder = f"{BASE_DIR}/import_export_goods/export_files/"
        body_files = f"{export_folder}export_goods_{str(datetime.now())[:-7].replace(' ', '_').replace(':', '_')}"
        with open(f"{body_files}.txt", "w",
                  encoding="utf-8") as file:
            file.write(str(data_csv))
        with open(f"{body_files}.csv", "w",
                  encoding="utf-8") as file:
            file.write(str(data_csv))
        with open(f"{body_files}.json", "w",
                  encoding="utf-8") as file:
            file.write(str(data_json))


if __name__ == "__main__":
    exp_obj = ProductResource()
    exp_obj.export_from_db()
    exp_obj.write_file()
