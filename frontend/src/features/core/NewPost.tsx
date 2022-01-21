import React, { useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import { AppDispatch } from "../../app/store";
import Modal from "react-modal";
import { MdAddAPhoto } from "react-icons/md";
import { Button, TextField, IconButton } from "@material-ui/core";
import styles from "./Core.module.css";
import { File } from "../types";
import {
  selectOpenNewPost,
  resetOpenNewPost,
  fetchPostStart,
  fetchPostEnd,
  fetchAsyncNewPost,
} from "../post/postSlice";

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

const NewPost: React.FC = () => {
  const dispatch: AppDispatch = useDispatch();
  const openNewPost = useSelector(selectOpenNewPost);
  const [image, setImage] = useState<File | null>(null);
  const [title, setTitle] = useState("");

  const handleEditPicture = () => {
    const inputFile = document.getElementById("imageInput");
    inputFile?.click();
  };

  const newPost = async (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault();
    const packet = { title: title, img: image };
    await dispatch(fetchPostStart());
    await dispatch(fetchAsyncNewPost(packet));
    await dispatch(fetchPostEnd());
    setImage(null);
    setTitle("");
    dispatch(resetOpenNewPost());
  };

  return (
    <>
      <Modal
        isOpen={openNewPost}
        onRequestClose={async () => {
          await dispatch(resetOpenNewPost());
        }}
        style={customStyles}
      >
        <form className={styles.core_signUp}>
          <h1 className={styles.core_title}>UwUgram</h1>
          <br />
          <TextField
            placeholder="Please enter caption"
            type="text"
            onChange={(e) => setTitle(e.target.value)}
          />
          <input
            type="file"
            id="imageInput"
            hidden={true}
            onChange={(e) => setImage(e.target.files![0])}
          />
          <br />
          <IconButton onClick={handleEditPicture}>
            <MdAddAPhoto />
          </IconButton>
          <br />
          <Button
            disabled={!title || !image}
            variant="contained"
            color="primary"
            onClick={newPost}
          >
            New post
          </Button>
        </form>
      </Modal>
    </>
  );
};

export default NewPost;
