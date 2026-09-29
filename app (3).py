import json
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Inventory Management System", page_icon="📦", layout="centered")

# -------- STATE (each visitor gets their own private inventory) --------
SAMPLE = {
    "laptop": {"quantity": 12, "price": 450.0},
    "mouse": {"quantity": 3, "price": 8.5},
    "keyboard": {"quantity": 25, "price": 15.0},
    "usb cable": {"quantity": 4, "price": 2.5},
}
if "inventory" not in st.session_state:
    st.session_state.inventory = dict(SAMPLE)
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
inventory = st.session_state.inventory

def table(data):
    rows = [{"Item": n.title(), "Quantity": d["quantity"], "Price": d["price"],
             "Status": "⚠ Low Stock" if d["quantity"] < 5 else "In Stock"} for n, d in data.items()]
    return pd.DataFrame(rows, columns=["Item", "Quantity", "Price", "Status"])

# -------- LOGIN --------
if not st.session_state.logged_in:
    st.title("📦 Inventory Management System")
    st.subheader("Login")
    user = st.text_input("Username")
    pwd = st.text_input("Password", type="password")
    st.caption("Demo login: username `admin`, password `1234`")
    if st.button("Login", type="primary"):
        try:  # optional: set USERNAME / PASSWORD in Streamlit secrets to change the demo login
            ok_user, ok_pwd = st.secrets["USERNAME"], st.secrets["PASSWORD"]
        except Exception:
            ok_user, ok_pwd = "admin", "1234"
        if user == ok_user and pwd == ok_pwd:
            st.session_state.logged_in = True
            st.rerun()
        else:
            st.error("Invalid credentials")
    st.stop()

# -------- MAIN APP --------
top, out = st.columns([4, 1])
top.title("📦 Inventory Management System")
if out.button("Logout"):
    st.session_state.logged_in = False
    st.rerun()

total_items = len(inventory)
low = sum(1 for d in inventory.values() if d["quantity"] < 5)
value = sum(d["quantity"] * d["price"] for d in inventory.values())
m1, m2, m3 = st.columns(3)
m1.metric("Items", total_items); m2.metric("Low stock", low); m3.metric("Stock value", f"${value:,.2f}")

tab_show, tab_add, tab_edit, tab_search, tab_data = st.tabs(
    ["📋 Inventory", "➕ Add", "✏️ Update / Delete", "🔍 Search", "💾 Save / Load"])

with tab_show:
    if inventory:
        st.dataframe(table(inventory), width="stretch", hide_index=True)
    else:
        st.info("Inventory is empty. Add an item.")

with tab_add:
    with st.form("add", clear_on_submit=True):
        name = st.text_input("Item name")
        qty = st.number_input("Quantity", min_value=0, step=1)
        price = st.number_input("Price", min_value=0.0, step=0.5, format="%.2f")
        if st.form_submit_button("Add Item"):
            if not name.strip():
                st.error("Please enter an item name.")
            else:
                inventory[name.strip().lower()] = {"quantity": int(qty), "price": float(price)}
                st.success(f"'{name.strip()}' added.")

with tab_edit:
    if not inventory:
        st.info("Nothing to edit yet.")
    else:
        sel = st.selectbox("Select item", sorted(inventory), format_func=str.title)
        cur = inventory[sel]
        with st.form("edit"):
            nq = st.number_input("Quantity", min_value=0, step=1, value=int(cur["quantity"]))
            np_ = st.number_input("Price", min_value=0.0, step=0.5, value=float(cur["price"]), format="%.2f")
            c1, c2 = st.columns(2)
            upd = c1.form_submit_button("Update Item", type="primary")
            dele = c2.form_submit_button("Delete Item")
        if upd:
            inventory[sel] = {"quantity": int(nq), "price": float(np_)}
            st.success(f"'{sel}' updated."); st.rerun()
        if dele:
            del inventory[sel]
            st.success(f"'{sel}' deleted."); st.rerun()

with tab_search:
    q = st.text_input("Search item name").strip().lower()
    if q:
        hits = {n: d for n, d in inventory.items() if q in n}
        st.dataframe(table(hits), width="stretch", hide_index=True) if hits else st.warning("Item not found")

with tab_data:
    st.write("Your inventory lives in this browser session. Download it to keep it, or upload a saved file.")
    st.download_button("⬇ Save inventory (JSON)", json.dumps(inventory, indent=2),
                       file_name="inventory.json", mime="application/json")
    up = st.file_uploader("Load inventory file (.json or .txt)", type=["json", "txt"])
    if up is not None and st.button("Load file"):
        try:
            data = json.load(up)
            assert all({"quantity", "price"} <= set(v) for v in data.values())
            st.session_state.inventory = data
            st.success("Inventory loaded."); st.rerun()
        except Exception:
            st.error("Invalid file format.")
