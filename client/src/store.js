import { configureStore, createSlice } from '@reduxjs/toolkit';

// redux stuff comes here

// Initial state
const initialState = {
  token: null,
  lang: 'english'
};

// Slice for token and lang
const userSlice = createSlice({
  name: 'user',
  initialState,
  reducers: {
    setToken: (state, action) => {
      state.token = action.payload;
    },
    setLang: (state, action) => {
      state.lang = action.payload;
    }
  }
});

export const { setToken, setLang } = userSlice.actions;

export const store = configureStore({
  reducer: {
    user: userSlice.reducer
  }
});

export default store;
