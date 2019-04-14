
data = {'addition': ['folder1', 'folder2'], 'deletion': ['folder3', 'folder4']}


table_title = ['Staging', 'Addition/Deletion', 'PROD']


function tableHeaderCreate(){
    var thead = document.createElement('thead') 
    var tr = document.createElement('tr')
    for (var j = 0; j < table_title.length; j++) {
        var th = document.createElement('th')   
        th.appendChild(document.createTextNode(table_title[j]))
        tr.appendChild(th)

    thead.appendChild(tr)
    }
    return thead
}

function fillColor(element_list, color){
    element_list.forEach(function(element) {
        element.style.color = 'black'
        element.style.backgroundColor = color
      });

}

function fillTableBody(changeList, tbody, update_status, color){
    for (var i=0; i<changeList.length; i++){
        let tr = document.createElement('tr')
        let th_prod = document.createElement('th')
        let th_staging= document.createElement('th')
        let th_diff = document.createElement('th')
        th_prod.appendChild(document.createTextNode(changeList[i]))
        th_staging.appendChild(document.createTextNode(changeList[i]))
        th_diff.appendChild(document.createTextNode(update_status))
        fillColor([th_prod, th_staging, th_diff], color)

        tr.appendChild(th_prod)
        tr.appendChild(th_diff)
        tr.appendChild(th_staging)
        tbody.appendChild(tr)
    }
}



function tableBodyCreate(){
    var tbody = document.createElement('tbody')
    let addition = data['addition']
    let deletion = data['deletion']
    fillTableBody(addition, tbody, 'Addition', 'green')
    fillTableBody(deletion, tbody, 'Deletion', 'red')
    return tbody

}

function clearTable(table){
    while (table.firstChild) {
        table.removeChild(table.firstChild);
    }
}

function tableCreate() {
    var tbl = document.getElementById('f_table')
    clearTable(tbl)
    thead = tableHeaderCreate()
    tbody = tableBodyCreate()
    tbl.appendChild(thead)
    tbl.appendChild(tbody)

}



  tableCreate();