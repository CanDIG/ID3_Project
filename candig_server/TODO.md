TODO

To set up candig server in travis, you're going to need to:

* create a fake referenceset that has a fasta that just covers chr1 from position 1...100
* pip install candig-ingest
* for each test case,
    * run ped_to_json.py on test_cases/[caseN]/ancestries.ped to get an ingest json file
    * ingest registry.db [caseN] [json file from above]
    * for each vcf in test_case_N
        * docker run -d c3genomics/candig_server -v config.py:/opt/candig_server/config.py -v registry.db:/opt/candig_server/registry.db --entrypoint candig_repo add-variantset [VCF].vcf.gz.tbi -R test-reference registry.db [case N] [sample name] [sample name] [VCF file]

Then start up candig-server:

docker run -d c3genomics/candig_server -v config.py:/opt/candig_server/config.py -v registry.db:/opt/candig_server/registry.db --entrypoint candig_server --host 0.0.0.0 --port 3000 -f /opt/candig_server/config.py

and run the test as before but with --use-candig-apis and with the candig server URL pointed to localhost:3000
