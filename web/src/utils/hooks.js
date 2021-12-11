import { useState, useCallback } from "react";
import { useEffect } from "react";

export function useInput(initValue) {
  const [values, setValues] = useState(initValue);

  const onChange = useCallback((e) => {
    const { name, value } = e.target;
    setValues((values) => ({ ...values, [name]: value }));
  }, []);

  const onFileChange = useCallback((e) => {
    setValues((values) => ({ ...values, ["file"]: e.taraget.file[0] }));
  }, []);

  const reset = useCallback(() => {
    setValues(initValue);
  }, [initValue]);
  return { values, onChange, onFileChange, reset };
}
//form field 입력받을 때 사용하는 훅.

export function useKeywords(mode, initValue) {
  const [values, setValues] = useState({ [mode]: initValue });

  const addKeyword = useCallback(
    (keyword) => {
      setValues((values) => ({ [mode]: [...values[mode], keyword] }));
    },
    [mode]
  );

  const deleteKeyword = useCallback(
    (deleteKeyword) => {
      let modified = values[mode];
      modified = modified.filter((keyword) => keyword !== deleteKeyword);
      setValues((values) => ({ ...values, [mode]: modified }));
    },
    [mode, values]
  );

  const reset = useCallback(() => setValues({}), []);

  return { values, addKeyword, deleteKeyword, reset };
}
//선택한 키워드 저장할 때 사용하는 훅.
//선호 키워드할 때는 mode prop을 'like'
//불호 키워드할 때는 mode props을 'hate'로 전달해주면 됨.

//!!구현해야 할 것. 다음 페이지 넘어갈 시 reset 호출 됨.
// => 리덕스에 키워드 저장할 것
// 새로운 검색 시 리덕스 값들 초기화하는 것 잊지 말 것!
export function useScript(url) {
  useEffect(()=> {
    const script = document.createElement('script');
    script.src = url;
    script.async = true;

    document.body.appendChild(script);

    return ()=> {
      document.body.removeChild(script);
    }
  }, [url]);
}