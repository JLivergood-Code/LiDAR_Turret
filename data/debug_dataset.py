import os

root = r"D:\CPE 350\data"

pcd_dir = os.path.join(root, "LCAS_20160523_1200_1218_pcd")
label_dir = os.path.join(root, "LCAS_20160523_1200_1218_labels")

print("pcd_dir:", pcd_dir)
print("label_dir:", label_dir)

print("pcd_dir exists:", os.path.isdir(pcd_dir))
print("label_dir exists:", os.path.isdir(label_dir))

if os.path.isdir(pcd_dir):
    print("\nPCD files found:")
    for f in os.listdir(pcd_dir):
        print("  ", f)

if os.path.isdir(label_dir):
    print("\nLabel files found:")
    for f in os.listdir(label_dir):
        print("  ", f)
