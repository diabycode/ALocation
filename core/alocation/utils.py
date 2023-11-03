import json

from django.http import HttpResponse
from django.http import Http404
from openpyxl import Workbook



EXPORT_FORMATS = ("pdf", "xlsx", "csv")


def export( serialized_data, export_type, sheet_title, filename ) -> HttpResponse or Http404:
    """ export data to a file """

    filename = filename + "." + export_type

    # if export_type == "pdf":
    #     return _pdf_export_response(serialized_data, filename)
    
    if export_type == "xlsx":
        return _xlsx_export_response(serialized_data, sheet_title, filename)
    
    if export_type == "csv":
        return _csv_export_response(serialized_data, filename)
    
    raise Http404


def _xlsx_export_response( serialized_data, sheet_title, filename ) -> HttpResponse:
    """ deserialize data and build an excel response from it """

    # deserialize data
    data_deserialized = json.loads(serialized_data)

    wb = Workbook()

    ws = wb.active

    ws.title = sheet_title

    column = [ c for c in data_deserialized[0]["fields"].keys() ]
    ws.append(column)

    for i, row in enumerate(data_deserialized, 1):
        data = [ i ]
        data.extend([d for d in row["fields"].values()])
        ws.append(data)

    wb.save(filename)

    with open(filename, "rb") as f:
        response = HttpResponse(f.read(), content_type="application/vnd.ms-excel")
        response["Content-Disposition"] = "attachment; filename={}".format(filename)

    return response


def _csv_export_response( serialized_data, filename ) -> HttpResponse:
    """ deserialize data and build an csv response from it """

    # deserialize data
    deserialized_data = json.loads(serialized_data)

    # add header
    column = [ c for c in deserialized_data[0]["fields"].keys() ]

    # write header
    with open(filename, "w") as f:
        f.write(",".join(column) + "\n")
    
    # write data rows
    with open(filename, "a") as f:
        for row in deserialized_data:
            
            data = []
            for d in row["fields"].values():
                if d is None:
                    d = ""
                data.append(str(d))

            f.write(",".join(data) + "\n")

    
    with open(filename, "rb") as f:
        response = HttpResponse(f.read(), content_type="text/csv")
        response["Content-Disposition"] = "attachment; filename={}".format(filename)

    return response


def _pdf_export_response( serialized_data, filename ): 
    pass


