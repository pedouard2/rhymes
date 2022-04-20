import { useEffect, useState, ChangeEvent, useMemo } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import './index.css';


let changes = 1
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
        }else{
           let result = await getWord(text) 
           if (result[text].length == 0) {
               result = await addWord(text)
           }
           values.push(result[text].map(item=> <span className={`${item.sound} s${item.stress}`} key={item.syllable}>{item.syllable}</span> ))
           words[text] = result[text]
           
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
    const [mirroredText, setMirroredText] = useState([])

    const handleChange = async (event: ChangeEvent<HTMLInputElement>) => {
        let n = event.target.value.split(/\s+/).length

        if (n !== changes){
            let t = event.target.value.split(/\s+/)
            
            let v = await colorize(t)
            setMirroredText(v)
           }
      
        setUserInput(event.target.value);
        changes = n
        
      };

    return (  
        <div className='container'>
            <div className='row'>
                <div className='col'>
                    <TextField
                    class="outlined-multiline-flexible col"
                    multiline
                    minRows={4}
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