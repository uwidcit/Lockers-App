function toast(message){
    M.toast({html:message})
}

async function sendRequest(url, method, data){
    try{ 
      let token = window.localStorage.getItem('access_token');
  
      let options = {
          method: method,
          headers: { 
            'Content-Type' : 'application/json',
            'Authorization' : `JWT ${token}`
          }
      };
  
      if(data)
        options.body = JSON.stringify(data);
  
      let response = await fetch(url, options);
        
      let result = await response.json();
      return result;
  
    }catch(error){
      return error;
    }
  }