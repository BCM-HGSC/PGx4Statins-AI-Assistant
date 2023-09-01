# -*- coding:utf-8 -*-
# Created by liwenw at 7/17/23

source_metadata_mapping = {
    "cpicslco1b1_PMC9035072.pdf":
        {"link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9035072/",
         "source": "Cooper-DeHoff RM, Niemi M, Ramsey LB, Luzum JA, Tarkiainen EK, Straka RJ, Gong L, Tuteja S, Wilke RA, Wadelius M, Larson EA, Roden DM, Klein TE, Yee SW, Krauss RM, Turner RM, Palaniappan L, Gaedigk A, Giacomini KM, Caudle KE, Voora D. The Clinical Pharmacogenetics Implementation Consortium Guideline for SLCO1B1, ABCG2, and CYP2C9 genotypes and Statin-Associated Musculoskeletal Symptoms. Clin Pharmacol Ther. 2022 May;111(5):1007-1021. doi: 10.1002/cpt.2557. Epub 2022 Mar 11. PMID: 35152405; PMCID: PMC9035072."},

    "cpicslco1b1supplement_PMC9035072.pdf":
        {"link": "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC9035072/",
         "source": "Supplemental Material - Cooper-DeHoff RM, Niemi M, Ramsey LB, Luzum JA, Tarkiainen EK, Straka RJ, Gong L, Tuteja S, Wilke RA, Wadelius M, Larson EA, Roden DM, Klein TE, Yee SW, Krauss RM, Turner RM, Palaniappan L, Gaedigk A, Giacomini KM, Caudle KE, Voora D. The Clinical Pharmacogenetics Implementation Consortium Guideline for SLCO1B1, ABCG2, and CYP2C9 genotypes and Statin-Associated Musculoskeletal Symptoms. Clin Pharmacol Ther. 2022 May;111(5):1007-1021. doi: 10.1002/cpt.2557. Epub 2022 Mar 11. PMID: 35152405; PMCID: PMC9035072."},

    "DPWG_August_2020.pdf":
            {"link": "https://api.pharmgkb.org/v1/download/file/attachment/DPWG_August_2020.pdf",
             "source": "Royal Dutch Pharmacists Association - Pharmacogenetics Working Group Guidelines" },

    "RNPGX_PMID28237404.pdf":
        {"link": "http://dx.doi.org/doi:10.1016/j.therap.2016.09.017",
         "source": "Fabien LamoureuxThomas Duflotthe French Network of Pharmacogenetics (RNPGX), Pharmacogenetics in cardiovascular diseases (2017), http://dx.doi.org/10.1016/j.therap.2016.09.017"},

    "Rosuvastatin_02_25_19_FDA.pdf":
        {"link": "https://www.accessdata.fda.gov/drugsatfda_docs/label/2018/021366s038lbl.pdf",
         "source": "FDA guidelines for CRESTOR (rosuvastatin calcium) tablets, Reference ID: 4347984"},

    "SLCO1B1_Diplotype_Phenotype_Mapping.csv":
        {"link": "",
         "source": "SLCO1B1 Diplotypes to Phenotypes Mapping"},
    "atorvastatin_SLCO1B1_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Atorvastatin CPIC Clinical Guidelines for SLCO1B1"},
    "fluvastatin_SLCO1B1_CYP2C9_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Fluvastatin CPIC Clinical Guidelines for SLCO1B1 and CYP2C9"},
    "lovastatin_SLCO1B1_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Lovastatin CPIC Clinical Guidelines for SLCO1B1"},
    "pitavastatin_SLCO1B1_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Pitavastatin CPIC Clinical Guidelines for SLCO1B1"},
    "pravastatin_SLCO1B1_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Pravastatin CPIC Clinical Guidelines for SLCO1B1"},
    "rosuvastatin_SLCO1B1_ABCG2_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Rosuvastatin CPIC Clinical Guidelines for SLCO1B1 and ABCG2"},
    "simvastatin_SLCO1B1_Phenotype_Pre_and_Post_Test_Alerts.csv":
        {"link": "",
         "source": "Simvastatin CPIC Clinical Guidelines for SLCO1B1"},

}

def pick_metadata(filename):
    if filename not in source_metadata_mapping:
        return None
    return source_metadata_mapping[filename]