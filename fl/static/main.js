document.addEventListener('DOMContentLoaded', () => {
    (document.querySelectorAll('.notification .delete') || []).forEach(($delete) => {
      $notification = $delete.parentNode;
  
      $delete.addEventListener('click', () => {
        $notification.parentNode.removeChild($notification);
      });
    });
  });

function hideModal() {
    document.getElementById('modal').style.display = 'none';
}

document.getElementById("deletePost").addEventListener("click", function(){
    document.getElementsById('modal').style.display = 'block';
});