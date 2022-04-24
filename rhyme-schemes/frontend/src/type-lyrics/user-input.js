import { useRef, useEffect, useState, ChangeEvent, useMemo } from 'react';
import './index.css';

let words = {}

const colorize =  async(arr) =>{
    let res = []
    for(let  i = 0; i<arr.length; i++){
        let text = arr[i]
        if (text ===""){
            continue
        }
        let values = []
        var w
        if (text in words){
            w = words[text]
            values.push(w.map(item=> <span className={`${item.sound} s${item.stress}`} key={item.syllable}>{item.syllable}</span> ))
        } else {
           let result = await getWord(text)
           
           if (result[text].length == 0) {
               result = await addWord(text)
           }

           if (result[text].length == 0){
               values.push(<span>{text}</span>)
           } else{
            values.push(result[text].map(item=> <span className={`${item.sound} s${item.stress}`} key={item.syllable}>{item.syllable}</span> ))
            words[text] = result[text]
           }
           
        }        
        let v = await Promise.all(values)
        
        res.push((<span className='word'>{v} </span>))
    }
   
    
    return res
}

async function getWord(w) {
    const resp  =  await fetch('api/get?' + new URLSearchParams({word: w}))
    const data =  await resp.json()
    return  data
    
}
async function addWord(w) {
    const resp  =  await fetch('api/add?' + new URLSearchParams({word: w}))
    const data =  await resp.json()
    return  data
    
}




const UserInput = () => {
  
    const [userInput, setUserInput] = useState("")
    const [mirroredText, setMirroredText] = useState("")

    const handleChange = async (event: ChangeEvent<HTMLInputElement>) => {
            setUserInput(event.target.value);
            setMirroredText(await colorize(event.target.value.split(/\s+/)))
        
      };

    return (  
        <div className='container'>
            <div className='row'>
                <div className='col' >
                    <textarea
                    class="md-textarea form-control col"
                    id="userInput"
                    rows={15}
                    value={userInput}
                    onChange={handleChange}/>
                </div>  
                <div className='col'>
                        {mirroredText}
                </div>

            </div>
                        
        </div>

       
    );
}
 
export default UserInput;