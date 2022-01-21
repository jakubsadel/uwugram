import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { AppDispatch } from "../../app/store";
import styles from "./Core.module.css";
import Modal from "react-modal";
import { MdAddAPhoto } from "react-icons/md";
import { Button, TextField, IconButton } from "@material-ui/core";
import { File } from "../types";
import {
  selectProfile,
  selectOpenProfile,
  resetOpenProfile,
  editNickName,
  fetchCredStart,
  fetchCredEnd,
  fetchAsyncUpdateProf,
} from "../auth/authSlice";

const customStyles = {
  content: {
    top: "50%",
    left: "50%",
    width: 280,
    height: 220,
    padding: "50px",
    transform: "translate(-50%, -50%)",
  },
};

const EditProfile: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const openProfile = useSelector(selectOpenProfile);
  const profile = useSelector(selectProfile);
  const [image, setImage] = useState<File | null>(null);

  const updateProfile = async (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    const packet = { id: profile.id, username: profile.username, img: image };

    await dispatch(fetchCredStart());
    await dispatch(fetchAsyncUpdateProf(packet));
    await dispatch(fetchCredEnd());
    await dispatch(resetOpenProfile());
  };

  const handlerEditPicture = () => {
    const inputFile = document.getElementById("imageInput");
    inputFile?.click();
  };

  return (
    <>
      <Modal
        isOpen={openProfile}
        onRequestClose={async () => {
          await dispatch(resetOpenProfile());
        }}
        style={customStyles}
      >
        <form className={styles.core_signUp}>
          <h1 className={styles.core_title}>UwUgram</h1>
          <br />
          <TextField
            placeholder="username"
            type="text"
            value={profile?.username}
            onChange={(e) => dispatch(editNickName(e.target.value))}
          />
          <input
            type="file"
            id="imageInput"
            hidden={true}
            onChange={(e) => setImage(e.target.files![0])}
          />
          <br />
          <IconButton onClick={handlerEditPicture}>
            <MdAddAPhoto />
          </IconButton>
          <br />
          <Button
            disabled={!profile?.username}
            variant="contained"
            color="primary"
            type="submit"
            onClick={updateProfile}
          >
            Update
          </Button>
        </form>
      </Modal>
    </>
  );
};

export default EditProfile;
