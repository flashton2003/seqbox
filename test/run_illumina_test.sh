set -e
set -o pipefail

#rm app/pa_seqbox_v2_test.db
#python scripts/test_no_web.py # creates db
#python scripts/seqbox_cmd.py add_groups -i scripts/groups_example.csv
#python scripts/seqbox_cmd.py add_projects -i scripts/projects_example.csv
python scripts/seqbox_cmd.py add_sample_sources -i scripts/illumina_test/sample_sources.csv
python scripts/seqbox_cmd.py add_samples -i scripts/illumina_test/samples_example.csv
python scripts/seqbox_cmd.py add_extractions -i scripts/illumina_test/extraction.csv
python scripts/seqbox_cmd.py add_raw_sequencing_batches -i scripts/illumina_test/raw_sequencing_batch.csv
python scripts/seqbox_cmd.py add_readsets -i scripts/illumina_test/illumina_read_sets_example.csv -c scripts/test_seqbox_config.yaml
