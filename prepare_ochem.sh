echo -e "smiles,logS\n" "$(grep New SolubilityCuration/CurationOChem/OChem_Clean.csv | awk -F, '{print $2, $3}' OFS=,)" > ochem_test.csv
