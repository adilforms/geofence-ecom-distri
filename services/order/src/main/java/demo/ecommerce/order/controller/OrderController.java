package demo.ecommerce.order.controller;

import demo.ecommerce.model.order.ShoppingCart;
import demo.ecommerce.order.service.OrderService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.security.access.prepost.PreAuthorize;
import org.springframework.security.oauth2.server.resource.authentication.JwtAuthenticationToken;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

@RestController
public class OrderController {

    @Autowired
    OrderService orderService;


    /**
     * Mono<ServerResponse>  return serialization error
     * Because: ServerResponse is the HTTP response type used by Spring WebFlux.fn, the functional variant of the reactive web framework.
     * it'snot supposed to use it within an annotated controller.
     * Solution use ResponseEntity
     */
    @PreAuthorize("hasAnyAuthority('SCOPE_client')")
    @PostMapping("/save") // save
    public Mono<ResponseEntity> saveOrder(@RequestBody ShoppingCart shoppingCart, JwtAuthenticationToken auth) {
        String email = auth.getTokenAttributes().get("client_id").toString();
        return orderService.saveShoppingCart(shoppingCart, email).
                flatMap(cart -> Mono.just(ResponseEntity.ok(cart)))
                .cast(ResponseEntity.class)
                .onErrorResume(ex -> Mono.just(ResponseEntity.status(HttpStatus.BAD_REQUEST).body(ex.getMessage())));
    }

    @PutMapping("/save")
    public Mono<ResponseEntity> updateOrder(JwtAuthenticationToken auth, @RequestBody ShoppingCart shoppingCart) {

        if (shoppingCart.getId() == null)
            throw new IllegalArgumentException("Cart id is required to update existing cart");
        String email = auth.getTokenAttributes().get("client_id").toString();
        return orderService.saveShoppingCart(shoppingCart, email).
                flatMap(cart -> Mono.just(ResponseEntity.ok(cart)))
                .cast(ResponseEntity.class)
                .onErrorResume(ex -> {
                    ex.printStackTrace();
                    return Mono.just(ResponseEntity.status(HttpStatus.BAD_REQUEST).body(ex.getMessage()));
                });
    }

    @PreAuthorize("hasAnyAuthority('SCOPE_client')")
    @GetMapping("/{orderId}")
    Mono<ShoppingCart> getOrder(@PathVariable("orderId") Long orderId, JwtAuthenticationToken auth) {
        String email = auth.getTokenAttributes().get("client_id").toString();
        return orderService.getShoppingCart(orderId, email);
    }

    @PreAuthorize("hasAnyAuthority('SCOPE_client')")
    @GetMapping("/list/user")
    Mono<Page<ShoppingCart>> getAllShoppingCart(JwtAuthenticationToken auth, @RequestParam Integer page, @RequestParam Integer pageSize) {
        String email = auth.getTokenAttributes().get("client_id").toString();
        return orderService.getUserShoppingCarts(email, PageRequest.of(page, pageSize));
    }



}
