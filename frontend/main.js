let projectUrl = "http://localhost:8000/api/projects/";

let getProject = () => {
  fetch(projectUrl)
    .then((response) => {
      console.log(response, 1);

      response.json();
    })
    .then((data) => {
      console.log(data);
    });
};
getProject();
