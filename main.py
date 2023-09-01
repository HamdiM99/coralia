

import streamlit as st
from Bio import PDB
import py3Dmol
from io import StringIO
from stmol import showmol
import os
import pandas as pd

folder = st.text_input("Path for the folder cotaining AlphFold results : ")


def get_pdb_files(folder_path):
    pdb_files = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdb"):
            pdb_files.append(filename)
    return pdb_files

######
import streamlit as st
from Bio import PDB


def parse_pdb_files(file_paths):
    # Create a PDB parser
    parser = PDB.PDBParser(QUIET=True)

    # Initialize an empty list to store parsed data
    pdb_data = []

    # Loop through the file paths and parse each PDB file
    columns = ["Chain", "Residue ID", "Residue Name", "Atom Name", "X", "Y", "Z"]

    pdb_data = []

    parser = PDB.PDBParser(QUIET=True)
    structure = parser.get_structure("protein", file_path)

    for model in structure:
        for chain in model:
            for residue in chain:
                for atom in residue:
                    pdb_data.append({
                        "Chain": chain.id,
                        "Residue ID": residue.id[1],
                        "Residue Name": residue.resname,
                        "Atom Name": atom.id,
                        "X": atom.coord[0],
                        "Y": atom.coord[1],
                        "Z": atom.coord[2]
                    })

    df = pd.DataFrame(pdb_data, columns=columns)
    return df



    # Create a DataFrame from the parsed data


    return df


######
def vis(pdb_file_path):
    parser = PDB.PDBParser(QUIET=True)
    model = parser.get_structure("protein", pdb_file_path)

    view = py3Dmol.view(width=800, height=400)

    pdb_io = PDB.PDBIO()
    pdb_stringio = StringIO()
    pdb_io.set_structure(model)
    pdb_io.save(pdb_stringio)
    pdb_string = pdb_stringio.getvalue()

    view.addModel(pdb_string, "pdb")


    style = st.sidebar.selectbox("style", ["cartoon", "line", "cross", "stick", "sphere"])

    view.setStyle({style: {"color": "spectrum"}})



    spin = st.sidebar.checkbox("Spin", value=False)
    if spin:
        view.spin(True)
    else:
        view.spin(False)
    view.zoomTo()

    showmol(view, height=500, width=800)

########


#Interface


########
if folder:

    st.title("AlphaFold 3D viz")

    files_names = get_pdb_files(folder)

    file_name = st.sidebar.selectbox("Choose the file you want to visualise", files_names)

    file_path = os.path.join(folder, file_name)

    pdb_files = get_pdb_files(folder)

    parsed_df = parse_pdb_files(pdb_files)

    # Display the DataFrame using st.dataframe
    st.dataframe(parsed_df)

    vis(file_path)

#####




