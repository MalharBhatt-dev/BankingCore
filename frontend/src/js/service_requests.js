async function createRequest(){

    const query_type = document.getElementById("query_type").value;
    const description = document.getElementById("description").value;

    if(!query_type){
        alert("Please select request type");
        return;
    }

    try{

        const data = await apiRequest(
            "/requests",
            "POST",
            {
                query_type: query_type,
                description: description
            }
        );

        alert(data.message);

    }
    catch(error){
        console.error("Request creation failed:",error);
    }

}