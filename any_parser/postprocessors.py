from bs4 import BeautifulSoup
import io
import csv


def run_convert(result, output_format):
    if output_format == "JSON":
        converter = _html_table_string_to_json
    elif output_format == "CSV":
        converter = _html_table_to_csv
    else:
        return result

    return [converter(table) for table in result]


def _html_table_string_to_json(html_string: str):
    soup = BeautifulSoup(html_string, "html.parser")
    table = soup.find("table")

    if not table:
        raise ValueError("No table found in the provided HTML string.")

    rows = table.find_all("tr")
    headers = [cell.get_text(strip=True) for cell in rows[0].find_all(["th", "td"])]

    result = []

    for row in rows[1:]:
        cells = row.find_all("td")
        row_object = {}

        for header, cell in zip(headers, cells):
            row_object[header] = cell.get_text(strip=True)

        result.append(row_object)

    return result


def _html_table_to_csv(html_string: str) -> str:
    soup = BeautifulSoup(html_string, "html.parser")
    table = soup.find("table")

    if not table:
        raise ValueError("No table found in the provided HTML string.")

    rows = table.find_all("tr")
    output = io.StringIO()
    csv_writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)

    for row in rows:
        cells = row.find_all(["th", "td"])
        csv_writer.writerow([cell.get_text(strip=True) for cell in cells])

    return output.getvalue()
