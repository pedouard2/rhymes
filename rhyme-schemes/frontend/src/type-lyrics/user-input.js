import { useEffect, useState, ChangeEvent } from 'react';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import './index.css';

let changes = 1
let defText = ""
let colors = ["red", "blue", "green"]

function getRandomcolor(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

function colorize(arr) {
    let res = []
    console.log(arr)
    for(let  i = 0; i<arr.length; i++){
        let text = arr[i]
        let c = getRandomcolor(colors)
        res.push((<span className='word' style={{'background-color': c}}>{text + " "}</span>))
    }
    return (<p>{res}</p>)
}
const UserInput = () => {

    const [userInput, setUserInput] = useState("")
    

    const handleChange = (event: ChangeEvent<HTMLInputElement>) => {
        let n = event.target.value.split(/\s+/).length

        if (n !== changes){
            // pass value to API target
            let t = event.target.value.split(/\s+/)
            defText = colorize(t)
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
                    <span>
                        {defText}  
                    </span>
                </div>

            </div>
                        
        </div>

       
    );
}
 
export default UserInput;