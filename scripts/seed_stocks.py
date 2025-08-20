import argparse
from pathlib import Path
from db_manager import import_stocks_from_csv


def main():
	parser = argparse.ArgumentParser(description="匯入台股清單到資料庫 (CSV)")
	parser.add_argument("csv", nargs="?", default="data/example_stocks.csv", help="CSV 檔案路徑 (預設: data/example_stocks.csv)")
	args = parser.parse_args()

	csv_path = Path(args.csv)
	if not csv_path.exists():
		print(f"找不到 CSV 檔案: {csv_path}")
		return 1

	inserted, updated, skipped = import_stocks_from_csv(str(csv_path))
	print(f"匯入完成: inserted+updated={inserted}, skipped={skipped}")
	return 0


if __name__ == "__main__":
	exit(main())
