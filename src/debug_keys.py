import pandas as pd

CASES="tables/cases_master.parquet"
OPINIONS="tables/opinions.parquet"
ISSUES="tables/issues.parquet"
VOTES="tables/votes.parquet"

def coerce(s): return pd.to_numeric(s, errors="coerce")

cm = pd.read_parquet(CASES)[["case_id","cl_cluster_id","case_name"]].copy()
cm["case_id"]=coerce(cm["case_id"]); cm["cl_cluster_id"]=coerce(cm["cl_cluster_id"])

op = pd.read_parquet(OPINIONS)[["case_id","cl_cluster_id"]].copy()
op["case_id"]=coerce(op["case_id"]); op["cl_cluster_id"]=coerce(op["cl_cluster_id"])

i  = pd.read_parquet(ISSUES)[["case_id","cl_cluster_id"]].copy()
i["case_id"]=coerce(i["case_id"]); i["cl_cluster_id"]=coerce(i["cl_cluster_id"])

j  = pd.read_parquet(VOTES)[["case_id","cl_cluster_id"]].copy()
j["case_id"]=coerce(j["case_id"]); j["cl_cluster_id"]=coerce(j["cl_cluster_id"])

print("Rows — cm/op/i/j:", len(cm), len(op), len(i), len(j))

# case_id overlaps
ci = set(cm["case_id"].dropna().unique())
oi = set(op["case_id"].dropna().unique())
ii = set(i["case_id"].dropna().unique())
ji = set(j["case_id"].dropna().unique())
print("case_id overlap: cm∩op:", len(ci & oi), "cm∩i:", len(ci & ii), "cm∩j:", len(ci & ji))

# cluster overlaps
cc = set(cm["cl_cluster_id"].dropna().unique())
oc = set(op["cl_cluster_id"].dropna().unique())
ic = set(i["cl_cluster_id"].dropna().unique())
jc = set(j["cl_cluster_id"].dropna().unique())
print("cluster overlap: cm∩op:", len(cc & oc), "cm∩i:", len(cc & ic), "cm∩j:", len(cc & jc))

# show the example you mentioned
ex_case = 6763
ex_cluster = 118474
print("\nExample check (case_id=6763, cl_cluster_id=118474)")
print("cm:", cm.loc[(cm.case_id==ex_case) | (cm.cl_cluster_id==ex_cluster)].head(3))
print("op:", op.loc[(op.case_id==ex_case) | (op.cl_cluster_id==ex_cluster)].head(3))
print("i :", i.loc[(i.case_id==ex_case) | (i.cl_cluster_id==ex_cluster)].head(3))
print("j :", j.loc[(j.case_id==ex_case) | (j.cl_cluster_id==ex_cluster)].head(3))