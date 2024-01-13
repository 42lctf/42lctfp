
import { useEffect, useRef, useState } from 'react';
import EasyMDE from 'easymde';


import hljs from 'highlight.js';
import 'highlight.js/styles/github.css';
import 'easymde/dist/easymde.min.css';

export function TestPage() {

    const [nickname, setNickname] = useState('');
    const renderAfterCalled = useRef(false);


    const text = useRef<HTMLTextAreaElement>(null);

    const [value, setValue] = useState('**Hello world!!!** <IFRAME SRC="javascript:javascript:alert(window.origin);"></IFRAME>');

    useEffect(() => {
        if (!renderAfterCalled.current) {


            const easyMDE = new EasyMDE({ element: text.current || undefined, renderingConfig: { hljs: hljs, codeSyntaxHighlighting: true, markedOptions: { sanitize: true } } });
            renderAfterCalled.current = true;

        }
    }, []);



    return (
        <div>
            dadaf
            <textarea ref={text} id="my-text-area" defaultValue={value} />
        </div>
    );
}