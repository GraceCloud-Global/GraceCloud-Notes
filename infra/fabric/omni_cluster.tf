resource "azurerm_kubernetes_cluster" "omni_cluster" {
  name                = "omni-continuum"
  location            = azurerm_resource_group.gracealone.location
  resource_group_name = azurerm_resource_group.gracealone.name
  dns_prefix          = "omnicore"
  default_node_pool {
    name       = "continuum"
    node_count = 6
    vm_size    = "Standard_B4ms"
  }
  identity {
    type = "SystemAssigned"
  }
}
