export interface File extends Blob {
  readonly lastModified: number;
  readonly name: string;
}

// authSlice.ts
export interface PROPS_AUTH {
  email: string;
  password: string;
}

export interface PROPS_PROFILE {
  id: number;
  username: string;
  img: File | null;
}

export interface PROPS_NICKNAME {
  username: string;
}

// postSlice.ts
export interface PROPS_NEWPOST {
  title: string;
  img: File | null;
}

export interface PROPS_LIKED {
  id: number;
  title: string;
  current: number[];
  // 新しくlikeしたuserのid
  new: number;
}

export interface PROPS_COMMENT {
  text: string;
  whichPost: number;
}

// Post.tsx
export interface PROPS_POST {
  postId: number;
  loginId: number;
  whosePost: number;
  title: string;
  imageUrl: string;
  liked: number[];
}
