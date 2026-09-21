document.addEventListener(
"DOMContentLoaded",
function(){


const search =
document.getElementById(
"topicSearch"
);


const status =
document.getElementById(
"statusFilter"
);


const category =
document.getElementById(
"categoryFilter"
);


const priority =
document.getElementById(
"priorityFilter"
);


const reset =
document.getElementById(
"resetFilters"
);



const rows =
document.querySelectorAll(
"#topicTableBody tr"
);




function filterTopics(){


    const searchValue =
    search.value.toLowerCase();


    const statusValue =
    status.value;


    const categoryValue =
    category.value;


    const priorityValue =
    priority.value;




    rows.forEach(
    row => {


        const title =
        row.dataset.title.toLowerCase();


        const rowStatus =
        row.dataset.status;


        const rowCategory =
        row.dataset.category;


        const rowPriority =
        row.dataset.priority;




        const visible =

        title.includes(searchValue)

        &&

        (!statusValue ||
        rowStatus === statusValue)

        &&

        (!categoryValue ||
        rowCategory === categoryValue)

        &&

        (!priorityValue ||
        rowPriority === priorityValue);




        row.style.display =
        visible ? "" : "none";


    });



}





search.addEventListener(
"keyup",
filterTopics
);


status.addEventListener(
"change",
filterTopics
);


category.addEventListener(
"change",
filterTopics
);


priority.addEventListener(
"change",
filterTopics
);



reset.addEventListener(
"click",
function(){


search.value="";

status.value="";

category.value="";

priority.value="";


filterTopics();


});


});